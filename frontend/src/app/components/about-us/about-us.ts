import { Component } from '@angular/core';
import {Footer} from "../footer/footer";
import {Home} from "../home/home";
import {Navigation} from "../navigation/navigation";

@Component({
  selector: 'app-about-us',
    imports: [
        Footer,
        Home,
        Navigation
    ],
  templateUrl: './about-us.html',
  styleUrl: './about-us.css',
})
export class AboutUs {

}
