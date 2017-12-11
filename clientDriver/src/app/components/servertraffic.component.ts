import { Component } from '@angular/core';
import { SocketService, Message } from '../services/serversocket.service';

@Component({
  selector: 'server-traffic',
  styleUrls: ["./servertraffic.component.scss"],
  templateUrl: "./servertraffic.component.html"
})

export class ServerTrafficComponent {
  public items: Object[] = [];

  constructor(private socketService: SocketService) {
    socketService.messages.subscribe(x => this.addItem(x));
  }

  addItem(item: Message) {
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
  }
}
