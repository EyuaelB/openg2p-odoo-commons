from odoo import api, fields, models


class SupersetDashboardConfig(models.Model):
    _name = "g2p.superset.dashboard.config"
    _description = "Superset Dashboard Configuration"

    name = fields.Char(string="Dashboard name", required=True)
    url = fields.Char(string="Dashboard URL", required=True)
    group_name = fields.Char("Group name", required=True)
    group = fields.Many2one("res.groups")
    menu_name = fields.Char("Menu title", required=True)
    menu = fields.Many2one("ir.ui.menu")
    action = fields.Many2one("ir.actions.client")

    @api.model
    def create(self, vals):
        group_vals = {
            "name": vals.get("group_name"),
            "category_id": self.env.ref("g2p_superset_dashboard.g2p_superset_dashboard_access_module").id,
            "implied_ids": [(4, self.env.ref("g2p_superset_dashboard.group_superset_user").id)],
        }
        group = self.env["res.groups"].create(group_vals)
        vals["group"] = group.id

        action_vals = {
            "name": f"{vals.get('menu_name')} Action",
            "tag": "g2p.superset_dashboard_embedded",
        }
        action = self.env["ir.actions.client"].create(action_vals)
        action_id = action.id

        menu_vals = {
            "name": vals.get("menu_name"),
            "parent_id": self.env.ref("g2p_superset_dashboard.menu_superset_dashboards").id,
            "action": f"ir.actions.client,{action_id}",
            "sequence": 1,
            "groups_id": [(6, 0, [int(group.id)])],  # Ensure IDs are integers
        }
        menu = self.env["ir.ui.menu"].create(menu_vals)
        vals["menu"] = menu.id

        if action_id:
            vals["action"] = action_id

        return super().create(vals)

    def unlink(self):
        for record in self:
            if not record.exists():
                continue
            if record.menu and record.menu.exists():
                record.menu.write({"groups_id": [(5, 0, [])]})

            if record.group and record.group.exists():
                if (
                    record.group.category_id.id
                    == self.env.ref("g2p_superset_dashboard.g2p_superset_dashboard_access_module").id
                ):
                    users = self.env["res.users"].search([("groups_id", "in", record.group.id)])
                    if users:
                        users.write({"groups_id": [(3, record.group.id)]})
                    record.group.unlink()

            if record.group and record.group.exists():
                record.group.unlink()

            if record.action and record.action.exists():
                record.action.unlink()

            if record.menu and record.menu.exists():
                record.menu.unlink()
        return super().unlink()

    def write(self, vals):
        if "menu_name" in vals:
            menu = self.env["ir.ui.menu"].browse(self.menu.id)
            if menu:
                menu.write({"name": vals["menu_name"]})

        if "group_name" in vals:
            group = self.env["res.groups"].browse(self.group.id)
            if group:
                group.write({"name": vals["group_name"]})
        return super().write(vals)
