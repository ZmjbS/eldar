import React, { PropTypes } from 'react';
import {connect} from 'react-redux'
import styles from './Header.css';

const mapStateToProps = ( state, props ) => {
	return {
		currentUser: state.users.currentUser,
		shifts: state.shifts.vaktir
	}
}

const mapDispatchToProps = ( dispatch ) => {
	return {
	}
}


class Header extends React.Component {

	//static defaultProps = {};
	//static propTypes = {};
	//state = {};

	//componentWillMount () {}
	//componentDidMount () {}
	//componentWillUnmount () {}
	//shouldComponentMount () { return true; }

	getText = (count) => {
		if(count === 0){
			return 'Þú ert ekki skráður á neinar vaktir en þú skráir þig á vaktir með því að smella á dagatalið';
		} else if(count < 5){
			return 'Velkominn í hópinn! Við miðum við 10-15 klst til að flugeldasalan gangi sem best fyrir sig :)';
		} else if( count < 10){
			return 'Þú ert skráður í ' + count + ' klst en vonandi skráir þú þig á fleiri vaktir ;)';
		} else if( count < 15){
			return 'Þitt framlag skiptir miklu máli til að gera flugeldasöluna mögulega. Þú ert skráður í ' + count + ' klst';
		} else if( count < 20 ){
			return 'Þú lætur ekkert stoppa þig. Þú ert skráður í ' + count + ' klst'
		} else if (count < 30){
			return 'Þú ert ofurmenni eða hefur einstaklega gaman af flugeldum! Þú ert skráður í ' + count + ' klst';
		} else {
			return 'Við höfum ekkert meira gáfulegt að segja við þig en þú tekur áramótin með trompi!';
		}
	}

	render () {
		const { currentUser: { nafn, netfang, simi }} = this.props;

		return (
			<div className={ styles.main }>
				<h1 className={ styles.title }>
					Vaktaskráningarkerfi HSSR
				</h1>
				<div className={ styles.user}>
					{ nafn } - { netfang } - { simi }
				</div>
				<div className={ styles.user}>
					Smellið á þær vaktir sem þið viljið taka. Allar breytingar vistast sjálfkrafa. Miðað er við að hver taki að sér 10-15 klst. Hægt er að breyta vöktum með því að smella á þær
				</div>
				<div className={styles.registrations }>{ this.getText(this.props.shifts ? this.props.shifts.length: 0)}</div>
			</div>
		);
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Header);

