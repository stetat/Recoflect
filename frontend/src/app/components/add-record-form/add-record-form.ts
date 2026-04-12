import {Component, model, signal} from '@angular/core';
import {FormsModule} from '@angular/forms';

enum Category {
  Food = 'Food',
  Transport = 'Transport',
  Bills = 'Bills',
  Entertainments = 'Entertainments',
  Healthcare = 'Healthcare',
  Education = 'Education',
  Service = 'Service',
  Subscription = 'Subscription',
  Other = 'Other'
}

enum Reflection {
  Happy = 'Happy',
  Neutral = 'Neutral',
  Regret = 'Regret'
}

enum Type {
  Income = 'Income',
  Expense = 'Expense',
}
@Component({
  selector: 'app-add-record-form',
  imports: [
    FormsModule
  ],
  templateUrl: './add-record-form.html',
  styleUrl: './add-record-form.css',
})
export class AddRecordForm {
  showAddRecordPage = model<boolean>(false);

  toggleAddRecordForm() {
    this.showAddRecordPage.set(!this.showAddRecordPage());
  }

  types = Object.values(Type);
  categories = Object.values(Category);
  reflections = Object.values(Reflection);

  record = {
    type: Type.Expense,
    category: Category.Food,
    amount: 0,
    date: new Date().toISOString().split('T')[0],
    reflection: Reflection.Neutral
  }

  onSubmit() {
    alert(`New record has been added. Record: ${this.record}`);
  }

}
