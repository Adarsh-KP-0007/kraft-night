# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_element(matrix, row_index, col_index):
    return matrix[row_index][col_index]
