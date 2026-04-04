import {Component, signal} from '@angular/core';
import {AddRecordForm} from '../add-record-page/add-record-form';

@Component({
  selector: 'app-add-record-btn',
  imports: [
    AddRecordForm
  ],
  templateUrl: './add-record-btn.html',
  styleUrl: './add-record-btn.css',
})
export class AddRecordBtn {
  showAddRecordPage = signal<boolean>(true);

  toggleAddRecordPage() {
    this.showAddRecordPage.set(!this.showAddRecordPage());
  }
}
