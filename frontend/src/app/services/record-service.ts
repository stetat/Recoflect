import {Injectable, signal} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, tap} from 'rxjs';

export interface RecordItem {
  id: string;
  type: 1 | 2;
  category: string;
  category_title: string;
  amount: string;
  date: string;
  reflection: 1 | 2 | 3;
}

export interface Category {
  id: string;
  title: string;
}

export interface CreateRecordPayload {
  type: 1 | 2;
  category: string;
  amount: number;
  date: string;
  reflection: 1 | 2 | 3;
}

@Injectable({
  providedIn: 'root',
})
export class RecordService {
  private apiUrl = 'http://localhost:8000/api/records/';
  private categoriesUrl = 'http://localhost:8000/api/categories/';
  income = signal<string | null>(localStorage.getItem("income"));
  expense = signal<string | null>(localStorage.getItem("expense"))
  net = signal<string | null>(localStorage.getItem("net"));
  dateStart = signal<string | null>(localStorage.getItem("dateStart"));
  dateEnd = signal<string | null>(localStorage.getItem("dateEnd"));
  constructor(private http: HttpClient) {}

  getSummary() {
    this.http.get<any>(`${this.apiUrl}summary/`).subscribe({
      next: (data) => {
        localStorage.setItem("income", data.income);
        localStorage.setItem("expense", data.expense);
        localStorage.setItem("net", data.net);
        localStorage.setItem("dateStart", data.period.start);
        localStorage.setItem("dateEnd", data.period.end);
        this.income.set(data.income);
        this.expense.set(data.expense);
        this.net.set(data.net);
        this.dateStart.set(data.dateStart);
        this.dateEnd.set(data.dateEnd);
      },
        error: err => {console.log(err)}
      });
  }

  getRecords(): Observable<RecordItem[]> {
    return this.http.get<RecordItem[]>(this.apiUrl);
  }

  createRecord(data: CreateRecordPayload): Observable<RecordItem> {
    return this.http.post<RecordItem>(this.apiUrl, data).pipe(
      tap(record => {
        this.getSummary();
      })
    );
  }

  deleteRecord(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl);
  }

  createCategory(title: string): Observable<Category> {
    return this.http.post<Category>(this.categoriesUrl, { title });
  }
}
