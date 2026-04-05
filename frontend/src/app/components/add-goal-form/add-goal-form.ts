import {Component, model, signal} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

enum Importance {
  Major = 'Major',
  Normal = 'Normal',
  Minor = 'Minor',
}

@Component({
  selector: 'app-add-goal-form',
    imports: [
        FormsModule,
        ReactiveFormsModule
    ],
  templateUrl: './add-goal-form.html',
  styleUrl: './add-goal-form.css',
})
export class AddGoalForm {
  showAddGoalForm = model<boolean>(true);
  private Objects: any;

  toggleAddGoalForm = () => this.showAddGoalForm.set(!this.showAddGoalForm());

  importanceTypes = Object.values(Importance);

  goal = {
    title: '',
    amount: null as any,
    deadline: new Date().toISOString().split('T')[0],
    importance: Importance.Normal,
  }

  onSubmit() {
    alert(`New record has been added. Record: ${this.goal}`);
  }
}
