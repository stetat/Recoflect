import { Routes } from '@angular/router';
import {Home} from './components/home/home';
import {AboutUs} from './components/about-us/about-us';
import {Contacts} from './components/contacts/contacts';


// pages (новые)
import { Login } from './pages/login/login';
import { Register} from './pages/register/register';
import { Records } from './pages/records/records';
import { Goals } from './pages/goals/goals';
import { Profile } from './pages/profile/profile';


export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },

  { path: 'home', component: Home},
  { path: 'login', component: Login},
  { path: 'register', component: Register },

  { path: 'records', component: Records},
  { path: 'goals', component: Goals },
  { path: 'profile', component: Profile},

  { path: 'about', component: AboutUs },
  { path: 'contacts', component: Contacts },
];

