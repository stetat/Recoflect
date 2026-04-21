import { CommonModule, DecimalPipe } from '@angular/common';
import { Component, computed, signal } from '@angular/core';

interface FamilyMember {
  id: number;
  username: string;
  role: 'parent' | 'child';
  weeklyIncome: number;
  weeklyExpense: number;
  limit?: number | null;
}

@Component({
  selector: 'app-family',
  standalone: true,
  imports: [CommonModule, DecimalPipe],
  templateUrl: './family.html',
  styleUrl: './family.css',
})
export class Family {
  familyName = signal('Recoflect Family');
  inviteCode = signal('A7K9P2');

  members = signal<FamilyMember[]>([
    {
      id: 1,
      username: 'Mom',
      role: 'parent',
      weeklyIncome: 180000,
      weeklyExpense: 65000,
      limit: null,
    },
    {
      id: 2,
      username: 'Dad',
      role: 'parent',
      weeklyIncome: 220000,
      weeklyExpense: 80000,
      limit: null,
    },
    {
      id: 3,
      username: 'Ali',
      role: 'child',
      weeklyIncome: 10000,
      weeklyExpense: 6500,
      limit: 12000,
    },
    {
      id: 4,
      username: 'Aya',
      role: 'child',
      weeklyIncome: 8000,
      weeklyExpense: 5200,
      limit: 10000,
    },
  ]);

  parents = computed(() => this.members().filter(member => member.role === 'parent'));
  children = computed(() => this.members().filter(member => member.role === 'child'));

  totalParentBalance = computed(() =>
    this.parents().reduce((sum, parent) => sum + this.getBalance(parent), 0)
  );

  totalChildExpense = computed(() =>
    this.children().reduce((sum, child) => sum + child.weeklyExpense, 0)
  );

  getBalance(member: FamilyMember): number {
    return member.weeklyIncome - member.weeklyExpense;
  }

  getLimitProgress(member: FamilyMember): number {
    if (!member.limit || member.limit <= 0) return 0;
    return Math.min((member.weeklyExpense / member.limit) * 100, 100);
  }

  getProgressClass(member: FamilyMember): string {
    const progress = this.getLimitProgress(member);

    if (progress >= 100) return 'danger';
    if (progress >= 75) return 'warning';
    return 'safe';
  }

  removeMember(id: number): void {
    this.members.update(list => list.filter(member => member.id !== id));
  }

  generateNewCode(): void {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';

    for (let i = 0; i < 6; i++) {
      code += chars[Math.floor(Math.random() * chars.length)];
    }

    this.inviteCode.set(code);
  }
}
