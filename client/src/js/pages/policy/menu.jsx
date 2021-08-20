import { Menu } from "antd";
import React from "react";

const { SubMenu } = Menu;

class PolicyMenu extends React.Component {
	render() {
		return (
			<Menu
				onClick={(e) => {this.props.onClick(e.key);}}
				mode="inline"
				defaultOpenKeys={["tax", "income_tax", "national_insurance", "benefits"]}
				defaultSelectedKeys={["main_rates"]}
			>
				<SubMenu key="tax" title="Tax">
					<SubMenu key="income_tax" title="Income Tax">
						<Menu.Item key="main_rates">Labour income</Menu.Item>
						<Menu.Item key="allowances">Allowances</Menu.Item>
						<Menu.Item key="it_alt">Structural</Menu.Item>
					</SubMenu>
					<SubMenu key="national_insurance" title="National Insurance">
						<Menu.Item key="employee_side">Employees</Menu.Item>
						<Menu.Item key="ni_alt">Structural</Menu.Item>
					</SubMenu>
				</SubMenu>
				<SubMenu key="benefits" title="Benefits">
					<Menu.Item key="universal_credit">Universal Credit</Menu.Item>
					<Menu.Item key="basic_income">Basic income</Menu.Item>
				</SubMenu>
			</Menu>
		);
	}
}

export default PolicyMenu;