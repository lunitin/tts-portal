
from flask import request, make_response, Blueprint, jsonify
from flask_restx import Resource, fields, Namespace, reqparse
from .models import User as db_User
from .models import Vehicle as db_Vehicle
from .models import Signal as db_Signal
from .models import Coverage as db_Coverage
from flask_restx import Api
import pandas as pd
import plotly.express as px
import plotly
NOT_FOUND = "{}: {} not found."


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='TTS-Portal Application API', validate=True)

#@api.errorhandler
#def sql_error(message, error):
#    return make_response(message, error)

# Namespace Delcarations for all objects, and Listed objects in db
# all urls will have the '/api' prefix (i.e. {{base_url}}/api/coverages/{{id}})
user_ns = Namespace('user', description="User related operations", path='/api')
users_ns = Namespace('users', description='Users related operations', path='/api')
vehicle_ns = Namespace('vehicle', description="Vehicle related operations", path='/api')
vehicles_ns = Namespace('vehicles', description='Vehicles related operations', path='/api')
signal_ns = Namespace('signal', description="Signal related operations", path='/api')
signals_ns = Namespace('signals', description='Signals related operations', path='/api')
coverage_ns = Namespace('coverage', description="Coverage related operations", path='/api')
coverages_ns = Namespace('coverages', description='Coverages related operations', path='/api')
dashboard_ns = Namespace('dashboard', description='Dashboard fetching operations', path='/api')

api.add_namespace(user_ns)
api.add_namespace(users_ns)
api.add_namespace(vehicle_ns)
api.add_namespace(vehicles_ns)
api.add_namespace(signal_ns)
api.add_namespace(signals_ns)
api.add_namespace(coverage_ns)
api.add_namespace(coverages_ns)
api.add_namespace(dashboard_ns)

user = users_ns.model('User', {
    'id': fields.Integer(required=False),
    'email_address': fields.String(default=None),
    'password': fields.String(default=None),
    'first_name': fields.String(default=None),
    'last_name': fields.String(default=None),
    'security_level': fields.Integer(default=None),
    'date_created': fields.Date(default=None),
    'date_last_login': fields.DateTime(default=None),
    'date_last_password_change': fields.DateTime(default=None)
})

vehicle = vehicles_ns.model('Vehicle', {
    'id': fields.Integer(required=False),
    'veh_id': fields.String(default=None),
    'delay': fields.Fixed(decimals=3,default=None),
    'red_arrival': fields.Boolean(default=None),
    'split_failure': fields.Boolean(default=None),
    'approach_direction': fields.String(default=None),
    'travel_direction': fields.String(default=None),
    'ett': fields.Fixed(decimals=3, default=None),
    'travel_time': fields.Fixed(decimals=3,default=None),
    'exit_status': fields.Boolean(default=None),
    'day': fields.Integer(default=None),
    'stops': fields.Boolean(default=None),
    'uturn': fields.Boolean(default=None),
    'entry_time': fields.DateTime(default=None),
    'exit_time': fields.DateTime(default=None),
    'signal_id': fields.Integer(default=None),
    'coverage_id': fields.Integer(default=None)
})

signal = signals_ns.model('Signal', {
    'id': fields.Integer(required=False),
    'coverage_id': fields.Integer(default=None),
    'vehicles': fields.List(fields.Integer, default=None)
})


coverage = coverages_ns.model('Coverage', {
    'id': fields.Integer(required=False),
    'coverage_name': fields.String(default="this"),
    'signals': fields.List(fields.Integer, default=None)
})


@dashboard_ns.route('/dashboard/arrivalPieChart')
class PieChart(Resource):
    @dashboard_ns.doc('Get arrivalPieChart information')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('signal', type=int)
        parser.add_argument('day', type=int)
        parser.add_argument('approach', type=str)
        parser.add_argument('tdirection', type=str)
        args = parser.parse_args()
        if args['approach'] == 'ALL': args['approach'] = None
        if args['tdirection'] == "ALL": args['tdirection'] = None
        vehicles, _ = db_Vehicle.search_by(SignalID=[args['signal']],
                                        TravelDirection=args['tdirection'],
                                        ApproachDirection=args['approach'],
                                        Day=[args['day']])
        df = pd.DataFrame.from_dict(vehicles)
        df.rename(columns = {'red_arrival': 'RedArrival'}, inplace = True)
        df.filter(['RedArrival'])
        df = df[df.RedArrival.isin([True, False])]

        arrivalCrossings = df.shape[0]

        #tempDf = df[df.RedArrival == 'No']
        #if tempDf.empty: lengthNo = 0
        #else: lengthNo = tempDf.size
        #if df.empty: lengthtotal = 1
        #else: lengthtotal = tempDf.size
        #greenArrivalRate = int((lengthNo / lengthtotal)*100)
    
        arrivalRates=px.pie(
            data_frame=df,
            names="RedArrival",
            color="RedArrival",
            hole=.5,
            title="Broward " + str(args['signal']) + " Arrival Rates",
            color_discrete_map={'True':'Red', 'False':'#90ee90'}
        )

        return plotly.io.to_json(arrivalRates)
        


@user_ns.route('/users/<int:id>')
class User(Resource):
    #@user_ns.marshal_with(user)
    @user_ns.doc('Get single user by id')
    def get(self, id):
        user = db_User.find_by_id(id)
        if user:
            return make_response(user.as_dict(), 200)
        else:
            return make_response(NOT_FOUND.format('user_id', id), 404)

    
    @user_ns.doc('Delete single user by id')
    def delete(self, id):
        user = db_User.find_by_id(id)
        if user:
            return user.delete_from_db()
        return make_response(NOT_FOUND.format('coverage ', id), 404)

        
    @user_ns.doc('Patch a single user by id')
    #@user_ns.marshal_with(user)
    def patch(self, id):
        coverage = db_Coverage.find_by_id(id)
        if coverage:
            new_data = request.get_json()
            coverage.id = new_data.get('coverage_id', coverage.id)
            coverage.coverage_name = new_data.get('coverage.coverage_name', coverage.coverage_name)
            bad_signal_id = new_coverage.add_signals(data.get('signals', None), delete_old=True)
            if bad_signal_id != 0:
                return(make_response(NOT_FOUND.format("signal_id", bad_signal_id), 404))

            return coverage.save_to_db()
        else:
            return make_response(NOT_FOUND.format('coverage ', id), 404)


@user_ns.route('/users/<int:id>/coverages')
class User_Coverages(Resource):
    @user_ns.doc("Get all User Coverages")
    def get(self, id):
        user = db_User.find_by_id(id)
        if user:
            return make_response(user.fetch_coverages(), 200)
        else:
            return make_response(NOT_FOUND.format('user_id', id), 404)
        


    @user_ns.doc("Add list of Coverages to User")
    def post(self, id):
        user = db_User.find_by_id(id)
        if user:
            data = request.get_json()
            coverages = data.get('coverages', None)
            bad_coverage_id = user.add_coverages(coverages)
            if bad_coverage_id != 0:
                return make_response(NOT_FOUND.format('coverage_id', bad_coverage_id), 404)
            else:
                return user.save_to_db()
        else:
            return make_response(NOT_FOUND.format('user_id', id), 404)

        
    @user_ns.doc("Remove list of Coverages to User")
    def delete(self, id):
        user = db_User.find_by_id(id)
        if user:
            data = request.get_json()
            coverages = data.get('coverages', None)
            bad_coverage_id = user.remove_coverages(coverages)
            if bad_coverage_id != 0:
                return make_response(NOT_FOUND.format('coverage_id', bad_coverage_id), 404)

            else:
                return user.save_to_db()
        else:
            return make_response(NOT_FOUND.format('user_id', id), 404)




@users_ns.route('/users')
class UserList(Resource):
    @users_ns.doc('Get all Users')
    #@users_ns.marshal_with(user, as_list=True)
    def get(self):
        return db_User.find_all()
    
    #@users_ns.marshal_with(user)
    @users_ns.expect(user)
    @users_ns.doc('Create a user')
    def post(self):
        new_user = db_User()
        data = request.get_json()
        new_user.id = data.get('id', None)
        new_user.email_address = data.get('email_address', None)
        new_user.password = data.get('password', None)
        new_user.first_name = data.get('first_name', None)
        new_user.last_name = data.get('last_name', None)
        new_user.security_level = data.get('security_level', None)
        new_user.date_created = data.get('date_created', None)
        new_user.date_last_login = data.get('last_login', None)
        new_user.data_last_password_change = data.get('data_last_password_change', None)
        if 'coverages' in data:
            bad_coverage_id = new_user.add_coverages((data.get('coverages'), None))
            if bad_coverage_id != 0:
                return(make_response(NOT_FOUND.format("coverage_id", bad_coverage_id), 404))

        return new_user.save_to_db()


@vehicle_ns.route('/vehicles/<int:id>')    
class Vehicle(Resource):
    #@vehicle_ns.marshal_with(vehicle)
    @vehicle_ns.doc('Get a single vehicle from id')
    def get(self, id):
        vehicle = db_Vehicle.find_by_id(id)
        if vehicle:
            return make_response(vehicle.as_dict(), 200)
        else:
            return make_response(NOT_FOUND.format('vehicle_id', id), 404)
    
    @vehicle_ns.doc('delete a single vehicle by id')
    def delete(self, id):
        vehicle = db_Vehicle.find_by_id(id)
        if vehicle:
            return vehicle.delete_from_db()
        return make_response(NOT_FOUND.format('vehicle_id', id), 404)

    
    @vehicle_ns.doc('patch a single vehicle by id')
    #@vehicle_ns.marshal_with(vehicle)
    def patch(self, id):
        vehicle = db_Vehicle.find_by_id(id)
        if vehicle:
            data = request.get_json()
            vehicle.id                  = data.get('id', vehicle.id)
            vehicle.veh_id              = data.get('veh_id', vehicle.id)
            vehicle.delay               = data.get('delay', vehicle.id)
            vehicle.red_arrival         = data.get('red_arrival', vehicle.id)
            vehicle.split_failure       = data.get('split_failure', vehicle.id)
            vehicle.approach_direction  = data.get('approach_direction', vehicle.id)
            vehicle.ett                 = data.get('ett', vehicle.id)
            vehicle.travel_time         = data.get('travel_time', vehicle.id)
            vehicle.exit_status         = data.get('exit_status', vehicle.id)
            vehicle.day                 = data.get('day', vehicle.id)
            vehicle.stops               = data.get('stops', vehicle.id)
            vehicle.uturn               = data.get('uturn', vehicle.id)
            vehicle.entry_time          = data.get('entry_time', vehicle.id)
            vehicle.exit_time           = data.get('exit_time', vehicle.id)
            vehicle.travel_direction    = data.get('travel_direction', vehicle.id)
            
            vehicle.coverage_id         = data.get('coverage_id', None)
            vehicle.signal_id           = data.get('signal_id', None)
            '''
            coverage = db_Coverage.find_by_id(data.get('coverage_id', None))
            if coverage:
                vehicle.coverage_id = coverage.id
            else: 
                return make_response(NOT_FOUND.format("coverage_id", data.get('coverage_id', None)), 404)


            signal = db_Signal.find_by_id(data.get('signal_id', None))
            if signal:
                vehicle.signal_id = signal.id
            else:
                return make_response(NOT_FOUND.format("signal_id", data.get('signal_id', None)), 404)
            '''

        return vehicle.save_to_db()
        
@vehicles_ns.route('/vehicles')
class Vehicle(Resource):
    @vehicles_ns.doc('Retrieve all vehicles that meet criteria')
    #@vehicles_ns.marshal_with(vehicle, as_list=True)
    def get(self):
        data = request.get_json()
        if data == None: vehicles = db_Vehicle.search_by()
        else:
            vehicles = db_Vehicle.search_by(
                data.get('EntryTime',None), data.get('ExitTime',None), data.get('TravelDirection',None), data.get('ApproachDirection',None),
                data.get('Day',None), data.get('SignalID',None), data.get('Stops', None), data.get('Uturn',None), data.get('DelayMinimum',None),
                data.get('DelayMaximum',None), data.get('RedArrival',None), data.get('ETTMinimum',None), data.get('ETTMaximum',None),
                data.get('TravelTimeMinimum',None), data.get('TravelTimeMaximum',None), data.get('ExitStatus',None)
                )
        
        return vehicles
    
    #@vehicles_ns.marshal_with(vehicle)
    @vehicles_ns.expect(vehicle)
    @vehicles_ns.doc('Create a vehicle instance')
    def post(self):
        new_vehicle = db_Vehicle()
        data = request.get_json()
        new_vehicle.id                  = data.get('id', None)
        new_vehicle.veh_id              = data.get('veh_id', None)
        new_vehicle.delay               = data.get('delay', None)
        new_vehicle.red_arrival         = data.get('red_arrival', None)
        new_vehicle.split_failure       = data.get('split_failure', None)
        new_vehicle.approach_direction  = data.get('approach_direction', None)
        new_vehicle.ett                 = data.get('ett', None)
        new_vehicle.travel_time         = data.get('travel_time', None)
        new_vehicle.exit_status         = data.get('exit_status', None)
        new_vehicle.day                 = data.get('day', None)
        new_vehicle.stops               = data.get('stops', None)
        new_vehicle.uturn               = data.get('uturn', None)
        new_vehicle.entry_time          = data.get('entry_time', None)
        new_vehicle.exit_time           = data.get('exit_time', None)
        new_vehicle.travel_direction    = data.get('travel_direction', None)
        new_vehicle.coverage_id         = data.get('coverage_id', None)
        new_vehicle.signal_id           = data.get('signal_id', None)

        '''
        coverage = db_Coverage.find_by_id(data.get('coverage_id', None))
        if coverage:
            new_vehicle.coverage_id = coverage.id
        else: 
            return make_response(NOT_FOUND.format("coverage_id", data.get('coverage_id', None)), 404)


        signal = db_Signal.find_by_id(data.get('signal_id', None))
        if signal:
            new_vehicle.signal_id = signal.id
        else:
            return make_response(NOT_FOUND.format("signal_id", data.get('signal_id', None)), 404)
        '''

        return new_vehicle.save_to_db()

@vehicles_ns.route('/vehicles/signals/<int:id>')
class VehicleList_by_Signal(Resource):
    #@vehicles_ns.marshal_with(vehicle, as_list=True)
    @vehicles_ns.doc("Fetch all vehicles based on Signal")
    def get(self, id):
        signal = db_Signal.find_by_id(id)
        if signal:
            return db_Vehicle.search_by(SignalID=[id])
        else:
            return make_response(NOT_FOUND.format('signal_id ', id), 404)


@vehicles_ns.route('/vehicles/coverages/<int:id>')
class VehicleList_by_Coverage(Resource):
    #@vehicles_ns.marshal_with(vehicle, as_list=True)
    @vehicles_ns.doc('Fetch all vehicles based on Coverage')
    def get(self, id):
        coverage = db_Coverage.find_by_id(id)
        if coverage:
            return db_Vehicle.search_by(CoverageID=[id])
        else:
            return make_response(NOT_FOUND.format('signal_id ', id), 404)


@signal_ns.route('/signals/<int:id>')
class Signal(Resource):
    @signal_ns.doc('Get a single signal from id')
    #@signal_ns.marshal_with(coverage)
    def get(self, id):
        signal = db_Signal.find_by_id(id)
        if signal:
            return make_response(signal.as_dict(), 200)
        else:
            return make_response(NOT_FOUND.format('signal_id ', id), 404)

    
    @signal_ns.doc('delete a single signal with id')
    def delete(self, id):
        signal = db_Signal.find_by_id(id)
        if signal:
            return signal.delete_from_db()
        else:
            return make_response(NOT_FOUND.format('signal_id ', id), 404)

        
    @signal_ns.doc('patch a single signal')
    #@signal_ns.marshal_with(coverage,)
    def patch(self, id):
        signal = db_Signal.find_by_id(id)
        if signal:
            new_data = request.get_json()
            signal.id = new_data.get('id', signal.id)
            signal.coverage_id = new_data.get('coverage_id', signal.coverage_id)
            bad_veh_id = signal.add_vehicles(data.get('vehicles', None), delete_old=True)
            if bad_veh_id != 0:
                return make_response(NOT_FOUND.format('vehicle_id', bad_veh_id, 404))

        else:
            return make_response(NOT_FOUND.format('signal_id', id), 404)

        return signal.save_to_db()
        
@signals_ns.route('/signals')
class SignalList(Resource):
    @signals_ns.doc('Get all Signals')
    #@signals_ns.marshal_with(signal, as_list=True)
    def get(self):
        return db_Signal.find_all()
    
    #@signals_ns.marshal_with(signal)
    @signals_ns.expect(signal)
    @signals_ns.doc('Create a signal')
    def post(self):
        new_signal = db_Signal()
        data = request.get_json()
        new_signal.id = data.get('id', None)
        if 'coverage_id' in data:
            coverage = db_Coverage.find_by_id(data.get('coverage_id', None))
            if coverage:
                new_signal.coverage_id = coverage.id
            else: 
                return(make_response(NOT_FOUND.format("coverage_id", data.get('coverage_id', None)), 404))
        if 'vehicles' in data:
            for veh_id in data['vehicles']:
                vehicle = db_Vehicle.find_by_id(veh_id)
                if vehicle:
                    new_signal.vehicles.append(vehicle)
                else:
                    return(make_response(NOT_FOUND.format("vehicle_id", veh_id), 404))

        return new_signal.save_to_db()
    
@coverage_ns.route('/coverages/<int:id>')
class Coverage(Resource):
    #@coverage_ns.marshal_with(coverage)
    @coverage_ns.doc('get a single covereage from id')
    def get(self, id):
        coverage = db_Coverage.find_by_id(id)
        if coverage:
            return make_response(coverage.as_dict(), 200)
        else:
            return make_response(NOT_FOUND.format('coverage_id',id), 404)

    
    @coverage_ns.doc('Delete a single coverage with id')
    def delete(self, id):
        coverage = db_Coverage.find_by_id(id)
        if coverage:
            return coverage.delete_from_db()
        return make_response(NOT_FOUND.format('coverage_id', id), 404)

        
    #@coverage_ns.marshal_with(coverage)
    @coverage_ns.doc("Patch a single coverage with id")
    def patch(self, id):
        coverage = db_Coverage.find_by_id(id)
        if coverage:
            new_data = request.get_json()
            coverage.id = new_data.get('coverage_id', coverage.id)
            coverage.coverage_name = new_data.get('coverage.coverage_name', coverage.coverage_name)
            bad_signal_id = new_coverage.add_signals(data.get('signals', None), delete_old=True)
            if bad_signal_id != 0:
                return(make_response(NOT_FOUND.format("signal_id", bad_signal_id), 404))

            return coverage.save_to_db()
        else:
            return make_response(NOT_FOUND.format('coverage_id', id), 404)


@coverages_ns.route('/coverages')
class CoverageList(Resource):
    @coverages_ns.doc('Get all Coverages')
    #@coverages_ns.marshal_with(coverage, as_list=True)
    def get(self):
        return db_Coverage.find_all()
    
    #@coverages_ns.marshal_with(coverage)
    @coverages_ns.expect(coverage)
    @coverages_ns.doc('Create a Coverage')
    def post(self):
        new_coverage = db_Coverage()
        data = request.get_json()
        new_coverage.id = data.get('id', None)
        new_coverage.coverage_name = data.get('coverage_name', None)
        bad_signal_id = new_coverage.add_signals(data.get('signals', []), delete_old=True)
        if bad_signal_id != 0:
                return(make_response(NOT_FOUND.format("signal_id", bad_signal_id), 404))

        return new_coverage.save_to_db() 