import {Component, computed, signal} from '@angular/core';

@Component({
  selector: 'app-home-goal',
  imports: [],
  templateUrl: './home-goal.html',
  styleUrl: './home-goal.css',
})
export class HomeGoal {
  goalReach = signal<number>(67.67);
  goalTitle = signal<string>("New car and a flat");
  currentBalance = signal<number>(123000);
  goalBalance = signal<number>(240000.67);
}
