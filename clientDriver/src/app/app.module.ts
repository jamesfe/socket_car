import { NgModule } from '@angular/core';
import { ClientCarMainComponent } from './ClientCarMain.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { ControlStickComponent } from './components/controlstick.component';
import { ServerTrafficComponent } from './components/servertraffic.component';

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule
    ],
    declarations: [
        ClientCarMainComponent,
        ControlStickComponent,
        ServerTrafficComponent
    ],
    bootstrap: [
        ClientCarMainComponent
    ]
})

export class AppModule {


}
