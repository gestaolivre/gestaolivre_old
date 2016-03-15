import {Component, OnInit} from 'angular2/core';
import {Empresa, EmpresaService} from './empresa.service';
import {RouteParams, Router} from 'angular2/router';
import {CanDeactivate, ComponentInstruction} from 'angular2/router';

@Component({
  templateUrl: 'app/empresa/empresa-detail.component.html',
  styleUrls: ['app/empresa/empresa-detail.component.css']
})
export class EmpresaDetailComponent implements OnInit, CanDeactivate {

  empresa: Empresa;
  editrazao_social: string;

  constructor(
    private _service: EmpresaService,
    private _router: Router,
    private _routeParams: RouteParams
    ) { }

  ngOnInit() {
    let cnpj = this._routeParams.get('cnpj');
    this._service.get(cnpj).subscribe(empresa => {
      if (empresa) {
        this.editrazao_social = empresa.razao_social;
        this.empresa = empresa;
      } else {
        this.gotoList();
      }
    });
  }

  routerCanDeactivate(next: ComponentInstruction, prev: ComponentInstruction): any {
    if (!this.empresa || this.empresa.razao_social === this.editrazao_social) {
      return true;
    }

    return new Promise<boolean>((resolve, reject) => resolve(window.confirm('Discard changes?')));
  }

  cancel() {
    this.editrazao_social = this.empresa.razao_social;
    this.gotoList();
  }

  save() {
    this.empresa.razao_social = this.editrazao_social;
    this._service.save(this.empresa).subscribe(() => this.gotoList(), (error) => console.log(error));
  }

  gotoList() {
    this._router.navigate(['EmpresaList']);
  }
}
