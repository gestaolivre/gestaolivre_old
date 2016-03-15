import {Component, OnInit} from 'angular2/core';
import {Empresa, EmpresaService} from './empresa.service';
import {ROUTER_DIRECTIVES} from 'angular2/router';

@Component({
  templateUrl: 'app/empresa/empresa-list.component.html',
  styleUrls: ['app/empresa/empresa-list.component.css'],
  directives: [ROUTER_DIRECTIVES]
})
export class EmpresaListComponent implements OnInit {
  empresas: Empresa[];
  constructor(private _service: EmpresaService) {}
  ngOnInit() {
    this._service.getAll().subscribe(empresas => this.empresas = empresas);
  }
}
