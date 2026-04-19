import {Component, computed, signal} from '@angular/core';
import { RouterLink } from  '@angular/router';
 @Component({
  selector: 'app-home-records',
  imports: [],
  templateUrl: './home-records.html',
  styleUrl: './home-records.css',
})
export class HomeRecords {
  dayStart = signal<string>("27");
  monthStart = signal<string>("03");
  dayEnd = signal<string>("04");
  monthEnd = signal<string>("04");

  income = signal<number>(53587);
  expense = signal<number>(12587);
  net = computed(() => this.income() - this.expense());
}
