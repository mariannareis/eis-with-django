#todas as classes estao aqui. Isso nao e necessario e nem muito 'bonito', vai ficar assim apenas inicialmente.
#Para resources => subclasses. (tal como marca e modelo, para produto...)
#Para nodes => decorators.
#Para movements => configuracao.

import sys, os
sys.path.append("home/mari/eis-examples-mari")
sys.path.append("/home/mari/eis-mari")

print sys.path
# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "eis-examples-mari.settings"

from django.db import models
from should_dsl import should
#from 'home/mari/eis-mari/domain/resource/work_item.py' import WorkItem
from domain.base.decorator import Decorator
from domain.node.person import Person
from domain.supportive.rule import rule
from domain.supportive.association_error import AssociationError
from domain.node.machine import Machine
from domain.supportive.contract_error import ContractError
from bank_system.resources.loan_request import LoanRequest
from bank_system.resources.loan import Loan
from bank_system.decorators.credit_analyst_decorator import CreditAnalystDecorator
from bank_system.decorators.bank_account_decorator import BankAccountDecorator
from bank_system.decorators.employee_decorator import EmployeeDecorator
from bank_system.rules.bank_system_rule_base import BankSystemRuleBase
from domain.supportive.rule_manager import RuleManager
from domain.resource.operation import operation

class BankAccountDecorator(models.Model, Decorator):
    '''Bank Account'''
    decoration_rules = ['should_be_instance_of_machine']

  #  def __init__(self, number):
    id = models.AutoField(primary_key=True)
    description = "A bank account decorator" #models.CharField(max_length=100)
    #log area for already processed resources
    log_area = {} #models.CharField(max_length=200)
    balance =  0 #models.IntegerField()
    #should it mask Machine.tag? decorated.tag = number?
    number = models.IntegerField()
    restricted = 0 #models.BooleanField()
    average_credit = 0 #models.IntegerField()
    def save(self, *args, **kwargs):
        super(BankAccountDecorator, self).save(*args, **kwargs)
        Decorator.__init__(self)

    @operation(category='business')
    def register_credit(self, value):
        ''' Register a credit in the balance '''
        self.balance += value

    @operation(category='business')
    def send_message_to_account_holder(self, message):
        ''' Sends a message to the account holder '''
        return message

#    @classmethod
#    @rule('association')
#    def rule_should_be_person_instance(self, decorated):
#        ''' Decorated object should be a Person '''
#        decorated |should| be_instance_of(Person)

#Um decorator Cliente envelopa um objeto Person.
#Se o cliente for uma empresa, ele envelopa uma Machine.
#Significa que suas association rules devem ser do tipo decorated |should| be_instance_of(Node) (que inclui Person e Machine)
#class CustomerDecorator(models.Model, Decorator): #decoracao concreta.... tem uma estancia de Person, que sera decorado'
#    id = models.AutoField(primary_key=True)
#    name = models.CharField(max_length=100)
#    address = models.CharField(max_length=200)

#    def save(self, *args, **kwargs):
#        super(CustomerDecorator, self).save(*args, **kwargs)
#        Decorator.__init__(self)

#    def decorate(self, decorated):
#        try:
#            CustomerDecorator.rule_should_be_person_instance(decorated)
#        except:
#            raise AssociationError('Person instance expected, instead %s passed' % type(decorated))
#        self.decorated = decorated
#        self.decorated.decorators[self.__doc__] = self

#    @classmethod
#    @rule('association')
#    def rule_should_be_person_instance(self, decorated):
#        ''' Decorated object should be a Person '''
#        decorated |should| be_instance_of(Person)

#class Brand(models.Model):
#    name = models.CharField(max_length=100)

#class ProductModel(models.Model):
#    brand = models.ForeignKey(Brand)
#    name = models.CharField(max_length=100)

##Produto = Resource (WorkItem)
#class Product(models.Model, WorkItem):
#    product_model = models.ForeignKey(ProductModel)
#    serial_number = models.CharField(max_length=100)

#    def save(self, *args, **kwargs):
#        super(Product, self).save(*args, **kwargs)
#        WorkItem.__init__(self)

#- Estoque(Decorator de No, com 'ponteiros' para as instancias de Produto)
#Note que movimentacoes de estoque sao representadas por um ou mais movements.
#Saida de item do estoque para o cliente => movement entre os nos Estoque e Cliente.
#class Stock(fk_product, in_stock)

#class Sale(fk_product, fk_cliente, data) ---> has_many products, belongs_to product / has_many clientes, belongs_to clientes
#Instancia de Process

#class Exchange(fk_product, fk_cliente, data, defeito_apresentado) ---> has_one product, belongs_to product
#Instancia de Process

