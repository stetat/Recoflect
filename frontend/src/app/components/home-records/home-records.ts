import {Component, computed, inject, signal} from '@angular/core';
import { RouterLink } from  '@angular/router';
import {RecordService} from '../../services/record-service';
 @Component({
  selector: 'app-home-records',
  imports: [],
  templateUrl: './home-records.html',
  styleUrl: './home-records.css',
})
export class HomeRecords {
   recordService = inject(RecordService);

  ngOnInit() {
    this.recordService.getSummary();
  }
  dateStart = this.recordService.dateStart();
  dateEnd = this.recordService.dateEnd();
  income = computed(()=> this.recordService.income() ?? 0);
  expense = computed(()=> this.recordService.expense() ?? 0);
  net = computed(()=> this.recordService.net() ?? 0);
}
