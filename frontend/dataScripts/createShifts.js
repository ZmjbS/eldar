const axios = require('axios');
const moment = require('moment');
const clone = require('lodash/clone');
const find = require('lodash/find');
const filter = require('lodash/filter');

var startDateTime = new Date(2018, 11, 27);
var endDateTime = new Date(2019, 0, 1);

Date.prototype.addHours = function ( h ) {
	this.setHours(this.getHours() + h);
	return this;
}

const getTegund = ( tegundir, start ) => {
	const hours = new Date(start).getHours();
	if ( hours >= 22 || hours < 10 ) {
		return find(tegundir, { nafn: 'næturvakt' })
	} else {
		return find(tegundir, { nafn: 'söluvakt' })
	}
}

const getSolustadir = async () => {
	const data = await (axios.get('http://127.0.0.1:8000/api/starfsstod/'))
	return filter(data.data, (starfsstod) => {
		return starfsstod.id <= 9;
	});
}

const getTegundir = async () => {
	const data = await (axios.get('http://127.0.0.1:8000/api/tegund/'))
	return data.data;
}

const getTimabil = async () => {
	const data = await (axios.get('http://127.0.0.1:8000/api/timabil/'))
	
	return filter(data.data, (timabil) => {
		const hefst = moment(timabil.hefst).hours();

		//console.log('timabil', timabil, hefst)
		return true
		//return hefst >= 7 && hefst < 10;
	});
}

const calculateHamark = ( solustadur, tegund, timabil ) => {
	const isNaeturvakt = tegund.name === 'næturvakt';
	const isSolustadur = !!solustadur.solustadur;

	if(solustadur.id === 10 && (moment(timabil.hefst).isBefore(new Date(2018, 11,28)) || moment(timabil.hefst).hours() >= 10)){
		return 0 // Smurbrauð
	} else if ( moment(timabil.hefst).isBefore(new Date(2018, 11, 27, 12)) ) {
		return 0;
	} else if ( moment(timabil.hefst).isAfter(new Date(2018, 11, 31, 18)) ) {
		return 0
	} else if ( isNaeturvakt && isSolustadur ) {
		return 2;
	} else if ( isNaeturvakt ) {
		return 0;
	}

	return solustadur.hamark;
}

const insertVaktForSolustadur = async ( solustadur, tegund, timabil ) => {
	try {
		const data = await axios.post('http://127.0.0.1:8000/api/vakt/', {
			timabil: timabil.id,
			starfsstod: solustadur.id,
			lagmark: tegund.name === 'næturvakt' ? 1 : 2,
			hamark: calculateHamark(solustadur, tegund, timabil),
			tegund: tegund.id
		});

		console.log('VAKT:', data.data);
		console.log('----');
	} catch ( e ) {
		console.log('ERROR', e.response.data);
	}

}

const insertVakt = async ( timabil, solustadir, tegundir ) => {

	const tegund = getTegund(tegundir, timabil.hefst);

	for ( let i = 0; i < solustadir.length; i++ ) {
		await insertVaktForSolustadur((solustadir[i]), tegund, timabil)
	}
}

const insertTimabil = async () => {
	console.log('STARTING TIMABIL...');
	try {
		while ( startDateTime < endDateTime ) {

			const hours = moment(startDateTime).hours();
			if ( hours >= 10 && hours < 23 ) {
				const data = await (axios.post('http://127.0.0.1:8000/api/timabil/', {
					hefst: startDateTime,
					lykur: clone(startDateTime).addHours(1)
				}))
				console.log('Timabil', data.data);
				console.log('----');
			}
			startDateTime.addHours(1);

		}

	} catch ( e ) {
		console.log('ERROR', e);
	}
	console.log('FINISHED TIMABIL');

}

const insertVaktir = async () => {
	console.log('STARTING VAKTIR');
	const tegundir = await getTegundir();

	const solustadir = await getSolustadir();

	const timabil = await getTimabil();

	console.log('solustadir', solustadir);

	console.log(timabil)

	// for ( let i = 0; i < timabil.length; i++ ) {
	// 	console.log('t', timabil[i]);

	// 	await insertVakt(timabil[i], solustadir, tegundir)
	// }
	console.log('FINISHED VAKTIR');
}

const start = async () => {
	console.log('STARTING...');

	//await insertTimabil();
	await insertVaktir();

}

start();
