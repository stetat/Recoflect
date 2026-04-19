import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GoalItem {
  id: string;
  title: string;
  amount: number;
  current_amount: number;
  deadline: string;
  importance: 1 | 2 | 3;
}

@Injectable({
  providedIn: 'root',
})
export class GoalService {
  private apiUrl = 'http://localhost:8000/api/goals/';

  constructor(private http: HttpClient) {}

  getGoals(): Observable<GoalItem[]> {
    return this.http.get<GoalItem[]>(this.apiUrl);
  }

  createGoal(data: Omit<GoalItem, 'id'>): Observable<GoalItem> {
    return this.http.post<GoalItem>(this.apiUrl, data);
  }

  updateGoal(id: string, data: Partial<GoalItem>): Observable<GoalItem> {
    return this.http.patch<GoalItem>(`${this.apiUrl}${id}/`, data);
  }

  deleteGoal(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}