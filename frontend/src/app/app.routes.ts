import { Routes } from '@angular/router';
import {Home} from './components/home/home';
import {AboutUs} from './components/about-us/about-us';
import {Contacts} from './components/contacts/contacts';
import {Login} from './pages/login/login';
import {Register} from './pages/register/register';
import { Records } from './pages/records/records'; 
import { Goals } from './pages/goals/goals';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home},
  { path: 'about', component: AboutUs},
  { path: 'contacts', component: Contacts},
  { path: 'login', component: Login},
  { path: 'register', component: Register},
  { path: 'records', component: Records },          
  { path: 'goals', component: Goals }, 
];
