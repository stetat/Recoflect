import { Component, model, OnInit, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Category, RecordService } from '../../services/record-service';

@Component({
  selector: 'app-add-record-form',
  imports: [FormsModule, CommonModule],
  templateUrl: './add-record-form.html',
  styleUrl: './add-record-form.css',
})
export class AddRecordForm implements OnInit {
  showAddRecordPage = model<boolean>(false);
  recordCreated = output<void>();

  categories: Category[] = [];
  newCategoryTitle = '';
  error = '';

  record = {
    type: 2 as 1 | 2,
    category: '',
    amount: null as number | null,
    date: new Date().toISOString().split('T')[0],
    reflection: 2 as 1 | 2 | 3,
  };

  constructor(private recordService: RecordService) {}

  ngOnInit(): void {
    this.recordService.getCategories().subscribe({
      next: cats => {
        this.categories = cats;
        if (cats.length > 0) this.record.category = cats[0].id;
      },
      error: () => this.error = 'Failed to load categories.',
    });
  }

  toggleAddRecordForm() {
    this.showAddRecordPage.set(false);
  }

  addCategory() {
    const title = this.newCategoryTitle.trim();
    if (!title) return;
    this.recordService.createCategory(title).subscribe({
      next: cat => {
        this.categories.push(cat);
        this.record.category = cat.id;
        this.newCategoryTitle = '';
        this.error = '';
      },
      error: () => this.error = 'Failed to create category.',
    });
  }

  onSubmit() {
    if (!this.record.category || !this.record.amount) return;

    this.recordService.createRecord({
      type: this.record.type,
      category: this.record.category,
      amount: this.record.amount,
      date: this.record.date,
      reflection: this.record.reflection,
    }).subscribe({
      next: () => {
        this.recordCreated.emit();
        this.showAddRecordPage.set(false);
      },
      error: () => this.error = 'Failed to save record.',
    });
  }
}
