import { Component, OnInit } from "@angular/core";

import { SocketService } from './services/serversocket.service';

@Component({
    selector: "socketcar",
    styleUrls: [ "./app.component.scss" ],
    templateUrl: "./app.component.html",
    providers: [ SocketService ]
})

export class AppComponent implements OnInit {

    public constructor(private controlService: SocketService) {}

    public ngOnInit(): void {}

}