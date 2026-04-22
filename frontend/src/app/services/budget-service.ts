import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface BudgetData {
  limit_amount: number | null;
  actual_spent: number;
  percent_used: number;
}

@Injectable({ providedIn: 'root' })
export class BudgetService {
  private apiUrl = 'http://localhost:8000/api/budget/';

  constructor(private http: HttpClient) {}

  getBudget(): Observable<BudgetData> {
    return this.http.get<BudgetData>(this.apiUrl);
  }

  setLimit(limit_amount: number): Observable<BudgetData> {
    return this.http.post<BudgetData>(this.apiUrl, { limit_amount });
  }
}
