import { Component } from '@angular/core';

@Component({
  selector: 'controlstick',
  template: `
    <div>
    <span><button name="zero">Zero</button></span>
    <span><button>Stop</button></span>
    <span><button>Inc Speed</button><button>Dec Speed</button></span>
    <span><button>Wheels Left</button><button>Wheels Right</button></span>
    </div>
  `
})

export class ControlStickComponent {

  constructor() { }

}
