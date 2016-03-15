import {Component} from 'angular2/core';
import {RouteConfig, RouterOutlet} from 'angular2/router';

import {EmpresaListComponent} from './empresa-list.component';
import {EmpresaDetailComponent} from './empresa-detail.component';
import {EmpresaService} from './empresa.service';

@Component({
  template: '<router-outlet></router-outlet>',
  providers: [EmpresaService],
  directives: [RouterOutlet]
})
@RouteConfig([
  {path:'/', name: 'EmpresaList', component: EmpresaListComponent, useAsDefault: true},
  {path:'/:cnpj', name: 'EmpresaDetail', component: EmpresaDetailComponent}
])
export class EmpresaRoot {
  constructor() {}
}
