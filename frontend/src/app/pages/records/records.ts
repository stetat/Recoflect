import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface RecordItem {
  id: string;
  type: number;
  category: string;
  amount: string;
  date: string;
  reflection: number;
}

@Component({
  selector: 'app-records',
  imports: [CommonModule],
  templateUrl: './records.html',
  styleUrl: './records.css'
})
export class Records {
  records: RecordItem[] = [
    {
      id: 'de499a88-a7a9-4968-a4ba-bb6cdc884eff',
      type: 2,
      category: 'Food',
      amount: '5000.00',
      date: '2026-04-16',
      reflection: 2
    },
    {
      id: '1e5cb123-4567-8901-abcd-ef1234567890',
      type: 1,
      category: 'Salary',
      amount: '250000.00',
      date: '2026-04-15',
      reflection: 1
    },
    {
      id: '3f7ac987-2222-3333-4444-555566667777',
      type: 2,
      category: 'Transport',
      amount: '1200.00',
      date: '2026-04-10',
      reflection: 3
    }
  ];

  getTypeLabel(type: number): string {
    return type === 1 ? 'Income' : 'Expense';
  }

  getReflectionLabel(reflection: number): string {
    if (reflection === 1) return 'Happy';
    if (reflection === 2) return 'Neutral';
    return 'Regret';
  }

  onEdit(record: RecordItem): void {
    console.log('Edit record:', record);
  }

  onDelete(id: string): void {
    this.records = this.records.filter(record => record.id !== id);
  }
}