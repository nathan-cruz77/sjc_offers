from datetime import datetime
import re

import scrapy

from sjc_offers.items import Offer


BASE_URL='http://servicos.sjc.sp.gov.br/sa/licitacoes/detalhe.aspx'


def squish(s):
    return re.sub(r'\s+', ' ', s.strip())


class OfferSpider(scrapy.Spider):
    name = 'offers'
    start_urls = [
        f'{BASE_URL}?sec=1,2&sit=1,2,3&mod=1,2,3,4,5,6,7,8,9,10,11,12,13,14&pag=1&pes='
    ]

    def parse(self, response):
        segments = response.xpath('//div[@id="ResultadoBusca"]').css('.panel-default')

        for segment in segments:
            yield self.parse_item(segment)

        url = self.next_page(response)

        if url:
            yield scrapy.Request(url, callback=self.parse)

    def parse_item(self, segment):
        offer = Offer()
        type, status, number = segment.css('.panel-heading').xpath('span/text()').extract()

        type = squish(type)

        offer['status'] = status
        offer['number'] = number
        offer['type'] = type
        offer['url'] = self.build_url(type, number)

        offer['description'] = self.get_description(segment)
        offer['max_value'] = self.get_max_value(segment, status)
        offer['start_date'] = self.get_start_date(segment, status)

        return offer

    def next_page(self, response):
        url = response.xpath('//a[text()="Próxima >"]/@href').extract_first()
        return f'{BASE_URL.rstrip("detalhe.aspx")}{url}'

    def build_url(self, type, number):
        return f'{BASE_URL}?sec=&sit=&mod={self.type_to_number(type)}&pag=1&pes={number}'

    def type_to_number(self, type):
        types = {
            'Carta Convite': 1,
            'Tomada de Preço': 2,
            'Pregão Presencial': 3,
            'Concorrência Pública': 4,
            'Pregão Eletrônico': 5,
            'Credenciamento/Pré qualificação': 6,
            'Leilão': 7,
            'Dispensa de Licitação': 8,
            'Seleção Baseada na Qualidade e Custo': 9,
            'Seleção Baseada na Qualificação dos Consultores': 10,
            'Licitação Pública Nacional': 11,
            'Regime Diferenciado de Contratação': 12,
            'Comparação de Preços': 13,
            'Licitação Pública Internacional': 14,
        }

        return types[type]

    def nth_body_line(self, segment, n):
        path = f'.//div[@class="form-control-static"][{n}]/span/text()'
        return segment.css('.panel-body').xpath(path).extract_first()

    def get_description(self, segment):
        return self.nth_body_line(segment, 1)

    def get_max_value(self, segment, status):
        if status != 'ABERTURA':
            return None

        value = self.nth_body_line(segment, 2).split()[-1]

        # Change decimal and thousand separator before parsing as float
        return float(value.replace('.', '').replace(',', '.'))

    def get_start_date(self, segment, status):
        line_from_status = {
            'ABERTURA': 3,
            'EM ANDAMENTO': 2,
            'FINALIZADA': 2,
        }

        line = self.nth_body_line(segment, line_from_status[status])

        if line == 'encerrado':
            return None

        try:
            date, _, time = line.split()[2:]
            return datetime.strptime(f'{date} {time.replace("h", ":")}', '%d/%m/%Y %H:%M')
        except ValueError:
            return None
