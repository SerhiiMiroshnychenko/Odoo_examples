import plotly
from odoo import models, fields, api
from datetime import datetime, timedelta
import logging
import base64
import io
import json
from datetime import datetime

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_history_data = fields.Text(
        string='Stock History Data',
        readonly=True
    )
    plotly_chart = fields.Text(
        string='Plotly Chart',
        compute='_compute_plotly_chart',
    )

    last_stock_update = fields.Datetime(
        string='Last Stock Update',
        readonly=True
    )

    def _compute_plotly_chart(self):
        for product in self:
            try:
                # Отримання історії
                if product.stock_history_data:
                    history_data = json.loads(product.stock_history_data)
                    history = [{
                        'date': datetime.strptime(item['date'], '%Y-%m-%d').date(),
                        'quantity': item['quantity']
                    } for item in history_data]
                else:
                    history = product.get_stock_history()

                if not history:
                    continue

                # Підготовка даних
                dates = [item['date'] for item in history]
                quantities = [item['quantity'] for item in history]
                dates_formatted = [date.isoformat() for date in dates]
                data = [{'x': dates_formatted, 'y': quantities}]
                product.plotly_chart = plotly.offline.plot(data,
                                                       include_plotlyjs=False,
                                                       output_type='div')
            except Exception as e:
                _logger.error(f"Error generating new plot: {str(e)}")
                product.plotly_chart = False

    def _serialize_datetime(self, dt):
        """Convert datetime to string for JSON serialization"""
        return dt.isoformat() if dt else None

    def _deserialize_datetime(self, dt_str):
        """Convert string to datetime from JSON deserialization"""
        return datetime.fromisoformat(dt_str) if dt_str else None

    def update_plotly_plot(self):
        for product in self:
            product._compute_plotly_chart()

    @api.depends('stock_move_ids', 'stock_move_ids.state', 'qty_available')
    def _compute_stock_history_data(self):
        for product in self:
            try:
                history = product.get_stock_history()
                # Convert datetime objects to strings for JSON serialization
                serializable_history = []
                for record in history:
                    serializable_history.append({
                        'date': self._serialize_datetime(record['date']),
                        'quantity': record['quantity']
                    })
                product.stock_history_data = json.dumps(serializable_history)
            except Exception as e:
                _logger.error(f"Error computing stock history data: {str(e)}")
                product.stock_history_data = "[]"

    def get_stock_history(self):
        """
        Get stock quantity history for the last year
        Returns: list of dictionaries containing date and quantity
        """
        self.ensure_one()
        today = fields.Date.today()
        year_ago = today - timedelta(days=365)

        # Get all stock moves for this product in the last year
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', self.id),
            ('date', '>=', year_ago),
            ('date', '<=', today),
            ('state', '=', 'done'),
        ], order='date asc')

        # Initialize result with starting quantity
        initial_qty = self.with_context(to_date=year_ago).qty_available
        result = [{
            'date': year_ago,
            'quantity': initial_qty
        }]

        current_qty = initial_qty
        for move in stock_moves:
            if move.location_dest_id.usage == 'internal' and move.location_id.usage != 'internal':
                # Incoming to stock
                current_qty += move.product_uom_qty
            elif move.location_id.usage == 'internal' and move.location_dest_id.usage != 'internal':
                # Outgoing from stock
                current_qty -= move.product_uom_qty

            result.append({
                'date': move.date.date(),
                'quantity': current_qty
            })

        # Add current quantity if last move was not today
        if not result or result[-1]['date'] != today:
            result.append({
                'date': today,
                'quantity': self.qty_available
            })

        return result