import { Component } from '@angular/core';
import { SocketService, Message, HealthCheck } from '../services/serversocket.service';

@Component({
  selector: 'server-traffic',
  styleUrls: ["./servertraffic.component.scss"],
  templateUrl: "./servertraffic.component.html"
})


export class ServerTrafficComponent {
  public items: Object[] = [];
  public health: HealthCheck = {
    left_motor: -999,
    right_motor: -999,
    steering: -999
  };

  constructor(private socketService: SocketService) {
    socketService.messages.subscribe(x => this.handleMessage(x));
  }

  handleMessage(item: Message) {
    this.addItem(item);
    if (item.health_check !== undefined) {
        this.health.left_motor = item.health_check.left_motor;
        this.health.right_motor = item.health_check.right_motor;
        this.health.steering = item.health_check.steering;
    }
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
