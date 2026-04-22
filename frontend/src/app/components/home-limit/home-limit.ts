import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BudgetData, BudgetService } from '../../services/budget-service';

@Component({
  selector: 'app-home-limit',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home-limit.html',
  styleUrl: './home-limit.css',
})
export class HomeLimit implements OnInit {
  budget = signal<BudgetData | null>(null);
  loading = signal(true);
  showForm = signal(false);
  saving = signal(false);
  newLimit = '';

  constructor(private budgetService: BudgetService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.budgetService.getBudget().subscribe({
      next: data => {
        this.budget.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false),
    });
  }

  percent(): number {
    return this.budget()?.percent_used ?? 0;
  }

  saveLimit(): void {
    const val = parseInt(this.newLimit, 10);
    if (!val || val <= 0) return;
    this.saving.set(true);
    this.budgetService.setLimit(val).subscribe({
      next: data => {
        this.budget.set(data);
        this.showForm.set(false);
        this.newLimit = '';
        this.saving.set(false);
      },
      error: () => this.saving.set(false),
    });
  }
}
