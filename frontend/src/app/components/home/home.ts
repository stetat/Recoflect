import {Component, signal} from '@angular/core';
import {Navigation} from '../navigation/navigation';
import {HomeLimit} from '../home-limit/home-limit';
import {HomeRecords} from '../home-records/home-records';
import {HomeGoal} from '../home-goal/home-goal';

@Component({
  selector: 'app-home',
  imports: [
    Navigation,
    HomeLimit,
    HomeRecords,
    HomeGoal
  ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  userName: string = "Darkhan";
  isLoggedIn = signal<boolean>(true);

}
