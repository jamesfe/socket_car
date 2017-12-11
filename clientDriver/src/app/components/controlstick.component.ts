import { Component } from '@angular/core';
import { SocketService, Message } from '../services/serversocket.service';
import { Observable } from "rxjs";

@Component({
  selector: 'control-stick',
  styleUrls: ["./controlstick.component.scss"],
  templateUrl: "./controlstick.component.html",
})

export class ControlStickComponent {
  public items: Object[] = [];

  constructor(private socketService: SocketService) {
    socketService.messages.subscribe(x => this.addItem(x));
  }

  addItem(item: Message) {
    console.log("storing item", item);
    if (item.type == "error") {
      let newMessage = {
        "type": item.type,
        "message": item.message };
      this.items.push(newMessage);
    }
    if (item.health_check !== undefined) {
      let newMessage = {
        "type": "health check",
        "message": JSON.stringify(item.health_check)
      };
      this.items.push(newMessage);
    }

    /* TODO: Move this code somewhere better. */
    if (this.items.length > 20) {
      this.items = this.items.slice(this.items.length - 20, this.items.length);
    }
    // TODO: Get template to update.
  }

  clickAction(action: string) {
    this.socketService.sendMessageBasedOnEvent(action);
  }
}
