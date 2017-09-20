import { Component } from '@angular/core';

@Component({
  selector: 'controlstick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html"
})

export class ControlStickComponent {

  constructor() { }

  zeroClick():any {
    console.log("zero click");
  }

}
