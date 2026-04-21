import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { GoalItem, GoalService } from '../../services/goal-service';

@Component({
  selector: 'app-home-goal',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './home-goal.html',
  styleUrl: './home-goal.css',
})
export class HomeGoal implements OnInit {
  loading = signal(true);
  goal = signal<GoalItem | null>(null);

  constructor(private goalService: GoalService) {}

  ngOnInit(): void {
    this.loadGoal();
  }

  loadGoal(): void {
    this.loading.set(true);
    this.goalService.getGoals().subscribe({
      next: goals => {
        this.goal.set(goals[0] ?? null);
        this.loading.set(false);
      },
      error: () => {
        this.goal.set(null);
        this.loading.set(false);
      },
    });
  }

  handleGoalCreated(goal: GoalItem): void {
    this.goal.set(goal);
  }

  goalReach(): number {
    const goal = this.goal();
    if (!goal?.amount) return 0;
    return Math.min(100, (goal.current_amount / goal.amount) * 100);
  }

  goalTitle(): string {
    return this.goal()?.title ?? 'No active goals yet';
  }

  currentBalance(): number {
    return this.goal()?.current_amount ?? 0;
  }

  goalBalance(): number {
    return this.goal()?.amount ?? 0;
  }

  hasGoal(): boolean {
    return !!this.goal();
  }
}
