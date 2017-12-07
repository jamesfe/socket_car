import { Component } from '@angular/core';
import { SocketService, Message } from '../services/serversocket.service';

@Component({
  selector: 'controlstick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {
  private turnval = 5; // how fast do we turn?
  private speedinc = 5; // how fast do we turn?

  constructor(private socketService: SocketService) {
    socketService.messages.subscribe(x => console.log(x));
  }

  clickAction(action: string) {
    var message: Message;
    switch (action) {
      case "left" || "a":
        message = {purpose: "turn", direction: "left", value: this.turnval}
        break;
      case "right" || "d":
        message = {purpose: "turn", direction: "right", value: this.turnval}
        break;
      case "incspeed" || "w":
        message = {purpose: "speed", left: true, right: true, value: this.speedinc}
        break;
      case "decspeed" || "s":
        message = {purpose: "speed", left: true, right: true, value: -1 * this.speedinc}
        break;
      case "zero" || "z":
        message = {purpose: "zero"}
        break;
      case "stop" || "q":
        message = {purpose: "stop"}
        break;
      default:
        console.log("Did not receive a valid action.");
    }
    console.log("Sending..." + message);
    var a = this.socketService.messages.next(message);
  }
}
