import { Component } from '@angular/core';
import { SocketService, Message } from '../services/serversocket.service';
import { Observable } from "rxjs";

@Component({
  selector: 'control-stick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {
  public items: String[] = [];

  constructor(private socketService: SocketService) {
    socketService.messages.subscribe(x => this.addItem(x));
  }

  addItem(item: Message) {
    console.log("storing item", item);
    if (item.type == "error") {
      let newMessage = item.type + " " + item.message;
      this.items.push(newMessage);
    }
    // TODO: Get template to update.
  }

  clickAction(action: string) {
    this.socketService.sendMessageBasedOnEvent(action);
  }
}
