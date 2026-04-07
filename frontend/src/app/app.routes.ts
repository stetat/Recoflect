import { Routes } from '@angular/router';
import {Home} from './components/home/home';
import {AboutUs} from './components/about-us/about-us';
import {Contacts} from './components/contacts/contacts';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home},
  { path: 'about', component: AboutUs},
  { path: 'contacts', component: Contacts},
];
