import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('front-end');

  constructor () {
    console.log("Logging Something")
    console.warn("Waring log")
    console.debug("Debug log")
    console.error("Error log")
    console.info("Info log")
  }
}
