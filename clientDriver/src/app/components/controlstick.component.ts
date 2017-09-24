import { Component } from '@angular/core';
import { SocketService } from '../services/serversocket.service';

@Component({
  selector: 'controlstick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {

  constructor(private socketService: SocketService) { }

  clickAction(action: string) {
    console.log("Sending...");
    this.socketService.sendGenMessage({body: "blah"});
    console.log(action);
  }
}
