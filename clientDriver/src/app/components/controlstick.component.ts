import { Component } from '@angular/core';
import { SocketService } from '../services/serversocket.service';

@Component({
  selector: 'controlstick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {

  private message = {
		purpose : 'turn',
		message: ''
	};

  constructor(private socketService: SocketService) { }

  clickAction(action: string) {
    console.log("Sending...");
    var a = this.socketService.messages.next(this.message);
    console.log(action);
  }
}
