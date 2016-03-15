import {describe, it, expect, beforeEachProviders, inject} from 'angular2/testing';
import {provide} from 'angular2/core';
import {EmpresaService} from './empresa.service';

describe('EmpresaService', () => {

  beforeEachProviders(() => [EmpresaService]);

  it('should get all empresas', inject([EmpresaService], (empresaService:EmpresaService) => {
    empresaService.getAll().subscribe(empresas => expect(empresas.length).toBe(1));
  }));

  it('should get one empresa', inject([EmpresaService], (empresaService:EmpresaService) => {
    empresaService.get('10711130000196').subscribe(empresa => expect(empresa.cnpj).toBe('10711130000196'));
  }));

});
