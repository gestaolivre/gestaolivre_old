import {Injectable}       from 'angular2/core';
import {Http, Response}   from 'angular2/http';
import {AuthHttp}         from 'angular2-jwt';
import {Observable}       from 'rxjs/Observable';

import { contentHeaders } from '../common/headers';

export class Empresa {
  constructor(public cnpj: string,
              public razao_social: string,
              public nome_fantasia: string) {
  }
}

@Injectable()
export class EmpresaService {
  private _url: string = '/api/geral/empresas';

  empresas: Empresa[];
  constructor(public authHttp: AuthHttp) {
  }

  getAll() {
    console.log(this._url);
    return this.authHttp.get(this._url)
      .map(res => {
        return <Empresa[]>res.json().results;
      })
      .catch(this.handleError);
  }

  get(cnpj: string) {
    return this.authHttp.get(this._url + '/' + cnpj)
      .map(res => <Empresa> res.json())
      .catch(this.handleError);
  }

  save(empresa: Empresa) {
    let body = JSON.stringify(empresa);
    return this.authHttp.put(this._url + '/' + empresa.cnpj, body, { headers: contentHeaders })
      .map(res => <Empresa>res.json())
      .catch(this.handleError);
  }

  private handleError(error: Response) {
    // in a real world app, we may send the error to some remote logging infrastructure
    // instead of just logging it to the console
    console.error(error);
    return Observable.throw(error.json().error || 'Server error');
  }
}
