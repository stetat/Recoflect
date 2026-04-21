import { Component, output, signal } from '@angular/core';
import { AddRecordForm } from '../add-record-form/add-record-form';

@Component({
  selector: 'app-add-record-btn',
  imports: [AddRecordForm],
  templateUrl: './add-record-btn.html',
  styleUrl: './add-record-btn.css',
})
export class AddRecordBtn {
  showAddRecordForm = signal<boolean>(false);
  recordCreated = output<void>();

  toggleAddRecordForm = () => this.showAddRecordForm.set(!this.showAddRecordForm());

  onRecordCreated() {
    this.recordCreated.emit();
  }
}
