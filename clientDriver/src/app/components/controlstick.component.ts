import { Component } from '@angular/core';
import { SocketService } from '../services/serversocket.service';
import { Observable } from "rxjs";

@Component({
  selector: 'control-stick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {

  constructor(private socketService: SocketService) {
  }

  clickAction(action: string) {
    this.socketService.sendMessageBasedOnEvent(action);
  }
}
