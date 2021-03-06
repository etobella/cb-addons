# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo import _, models


class AccountInvoiceIntegrationMethod(models.Model):
    _inherit = "account.invoice.integration.method"

    def integration_values(self, invoice):
        res = super().integration_values(invoice)
        if self == self.env.ref("invoice_integration_email.integration_email"):
            res.update(self.email_integration_values(invoice))
        return res

    def get_email_integration_action(self, invoice):
        return invoice.partner_id.invoice_report_email_id or self.env.ref(
            "account.account_invoices"
        )

    def email_integration_values(self, invoice):
        action = self.get_email_integration_action(invoice)
        content, content_type = action.render(invoice.ids)
        attachment = False
        if action.attachment:
            attachment = action.retrieve_attachment(invoice)
        if not attachment:
            fname = _("Invoice %s") % invoice.number
            mimetype = False
            if content_type == "pdf":
                mimetype = "application/pdf"
            if content_type == "xls":
                mimetype = "application/vnd.ms-excel"
            if content_type == "xlsx":
                mimetype = (
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            if content_type == "csv":
                mimetype = "text/csv"
            if content_type == "xml":
                mimetype = "application/xml"
            attachment = self.env["ir.attachment"].create(
                {
                    "name": fname,
                    "datas": base64.b64encode(content),
                    "datas_fname": fname,
                    "res_model": "account.invoice",
                    "res_id": invoice.id,
                    "mimetype": mimetype,
                }
            )
        return {"attachment_id": attachment.id}
