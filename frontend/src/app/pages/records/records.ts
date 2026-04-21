import { Component, computed, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecordItem, RecordService } from '../../services/record-service';
import { AddRecordBtn } from '../../components/add-record-btn/add-record-btn';

@Component({
  selector: 'app-records',
  imports: [CommonModule, AddRecordBtn],
  templateUrl: './records.html',
  styleUrl: './records.css',
  providers: [RecordService],
})
export class Records implements OnInit {
  loading = signal<boolean>(true);
  error = signal<string | null>(null);
  records = signal<RecordItem[]>([]);

  income  = computed(() => this.records().filter(r => r.type === 1));
  expense = computed(() => this.records().filter(r => r.type === 2));

  constructor(private recordService: RecordService) {}

  ngOnInit(): void {
    this.loadRecords();
  }

  loadRecords(): void {
    this.loading.set(true);
    this.error.set(null);
    this.recordService.getRecords().subscribe({
      next: (data: RecordItem[]) => {
        this.records.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load records. Make sure you are logged in.');
        this.loading.set(false);
      },
    });
  }

  getReflectionLabel(reflection: number): string {
    if (reflection === 1) return 'Happy';
    if (reflection === 2) return 'Neutral';
    return 'Regret';
  }

  onDelete(id: string): void {
    this.recordService.deleteRecord(id).subscribe({
      next: () => this.records.update(list => list.filter(r => r.id !== id)),
      error: () => this.error.set('Failed to delete record.'),
    });
  }
}
