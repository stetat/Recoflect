import {Component, signal} from '@angular/core';
import {AddRecordForm} from '../add-record-form/add-record-form';

@Component({
  selector: 'app-add-record-btn',
  imports: [
    AddRecordForm
  ],
  templateUrl: './add-record-btn.html',
  styleUrl: './add-record-btn.css',
})
export class AddRecordBtn {
  showAddRecordForm = signal<boolean>(false);

  toggleAddRecordForm = () => this.showAddRecordForm.set(!this.showAddRecordForm());

}
