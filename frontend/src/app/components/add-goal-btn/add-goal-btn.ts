import {Component, signal} from '@angular/core';
import {RouterLink} from '@angular/router';
import {AddGoalForm} from '../add-goal-form/add-goal-form';

@Component({
  selector: 'app-add-goal-btn',
  imports: [
    RouterLink,
    AddGoalForm
  ],
  templateUrl: './add-goal.html',
  styleUrl: './add-goal.css',
})
export class AddGoalBtn {
  showAddGoalForm = signal<boolean>(true);

  toggleAddGoalForm = () => this.showAddGoalForm.set(!this.showAddGoalForm());
}
