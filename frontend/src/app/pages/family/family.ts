import { CommonModule, DecimalPipe } from '@angular/common';
import { Component, computed, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  FamilyData,
  FamilyJoinRequest,
  FamilyMember,
  FamilyService,
} from '../../services/family-service';

@Component({
  selector: 'app-family',
  standalone: true,
  imports: [CommonModule, DecimalPipe, FormsModule],
  templateUrl: './family.html',
  styleUrl: './family.css',
})
export class Family implements OnInit {
  loading = signal(true);
  submitting = signal(false);
  error = signal<string | null>(null);
  info = signal<string | null>(null);
  family = signal<FamilyData | null>(null);
  pendingJoinRequest = signal<FamilyJoinRequest | null>(null);

  createFamilyName = '';
  inviteCodeInput = '';
  desiredRole: 1 | 2 = 2;

  constructor(private familyService: FamilyService) {}

  ngOnInit(): void {
    this.loadFamily();
  }

  members = computed(() => this.family()?.members ?? []);

  familyName = computed(() => this.family()?.family_name ?? '');
  inviteCode = computed(() => this.family()?.invite_code ?? '');
  canManageFamily = computed(() => this.family()?.current_user_role === 1);
  currentUserId = computed(() => this.family()?.current_user_id ?? null);
  joinRequests = computed(() => this.family()?.join_requests ?? []);

  parents = computed(() =>
    this.members().filter(member => member.role === 1)
  );

  children = computed(() =>
    this.members().filter(member => member.role === 2)
  );

  totalParentBalance = computed(() =>
    this.parents().reduce((sum, parent) => sum + this.getBalance(parent), 0)
  );

  totalChildExpense = computed(() =>
    this.children().reduce((sum, child) => sum + child.weekly_expense, 0)
  );

  getBalance(member: FamilyMember): number {
    return member.weekly_income - member.weekly_expense;
  }

  getLimitProgress(member: FamilyMember): number {
    if (!member.limit || member.limit <= 0) return 0;
    return Math.min((member.weekly_expense / member.limit) * 100, 100);
  }

  getMemberName(member: FamilyMember): string {
    return member.first_name?.trim() || member.username;
  }

  getRoleLabel(member: FamilyMember): string {
    if (member.role === 1) return 'Parent';
    if (member.role === 2) return 'Child';
    return 'Member';
  }

  canRemoveMember(member: FamilyMember): boolean {
    return this.canManageFamily() && member.id !== this.currentUserId();
  }

  loadFamily(): void {
    this.loading.set(true);
    this.error.set(null);

    this.familyService.getFamily().subscribe({
      next: response => {
        if ('family' in response) {
          this.family.set(response.family);
          this.pendingJoinRequest.set(response.pending_join_request ?? null);
        } else {
          this.family.set(response);
          this.pendingJoinRequest.set(null);
        }
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load family data.');
        this.loading.set(false);
      },
    });
  }

  createFamily(): void {
    const familyName = this.createFamilyName.trim();
    if (!familyName) return;

    this.submitting.set(true);
    this.error.set(null);
    this.info.set(null);

    this.familyService.createFamily(familyName).subscribe({
      next: family => {
        this.family.set(family);
        this.createFamilyName = '';
        this.pendingJoinRequest.set(null);
        this.submitting.set(false);
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to create family.');
        this.submitting.set(false);
      },
    });
  }

  joinFamily(): void {
    const inviteCode = this.inviteCodeInput.trim().toUpperCase();
    if (!inviteCode) return;

    this.submitting.set(true);
    this.error.set(null);
    this.info.set(null);

    this.familyService.joinFamily(inviteCode, this.desiredRole).subscribe({
      next: response => {
        this.pendingJoinRequest.set(response.pending_join_request);
        this.info.set(response.detail);
        this.inviteCodeInput = '';
        this.desiredRole = 2;
        this.submitting.set(false);
      },
      error: err => {
        this.error.set(
          err?.error?.invite_code?.[0] ?? err?.error?.detail ?? 'Failed to join family.'
        );
        this.submitting.set(false);
      },
    });
  }

  getDesiredRoleLabel(role: number): string {
    if (role === 1) return 'Parent';
    if (role === 2) return 'Child';
    return 'Member';
  }

  getProgressClass(member: FamilyMember): string {
    const progress = this.getLimitProgress(member);

    if (progress >= 100) return 'danger';
    if (progress >= 75) return 'warning';
    return 'safe';
  }

  removeMember(id: string): void {
    this.familyService.removeMember(id).subscribe({
      next: family => {
        this.family.set(family);
        this.error.set(null);
        this.info.set(null);
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to remove member.');
      },
    });
  }

  generateNewCode(): void {
    this.familyService.regenerateInviteCode().subscribe({
      next: family => {
        this.family.set(family);
        this.error.set(null);
        this.info.set('Invite code refreshed.');
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to regenerate invite code.');
      },
    });
  }

  leaveFamily(): void {
    this.familyService.leaveFamily().subscribe({
      next: () => {
        this.family.set(null);
        this.pendingJoinRequest.set(null);
        this.error.set(null);
        this.info.set(null);
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to leave family.');
      },
    });
  }

  approveRequest(requestId: string): void {
    this.familyService.approveRequest(requestId).subscribe({
      next: family => {
        this.family.set(family);
        this.error.set(null);
        this.info.set('Request approved.');
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to approve request.');
      },
    });
  }

  rejectRequest(requestId: string): void {
    this.familyService.rejectRequest(requestId).subscribe({
      next: family => {
        this.family.set(family);
        this.error.set(null);
        this.info.set('Request rejected.');
      },
      error: err => {
        this.error.set(err?.error?.detail ?? 'Failed to reject request.');
      },
    });
  }
}
