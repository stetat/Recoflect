import {Component, signal} from '@angular/core';
import {Navigation} from '../navigation/navigation';
import {HomeLimit} from '../home-limit/home-limit';
import {HomeRecords} from '../home-records/home-records';
import {HomeGoal} from '../home-goal/home-goal';
import {AddGoalBtn} from '../add-goal-btn/add-goal-btn';
import {AddRecordBtn} from '../add-record-btn/add-record-btn';
import {Footer} from '../footer/footer';

@Component({
  selector: 'app-home',
  imports: [
    Navigation,
    HomeLimit,
    HomeRecords,
    HomeGoal,
    AddGoalBtn,
    AddRecordBtn,
    Footer
  ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  userName: string = "Darkhan";
  isLoggedIn = signal<boolean>(true);

}
