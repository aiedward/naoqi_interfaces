from naoqi_interfaces.events.event_abstractclass import EventAbstractclass
from naoqi_interfaces.control.event_spinner import EventSpinner
import argparse


class SingleEvent(EventAbstractclass):
    # Overriding the abstract callback from EventAbstractclass
    def callback(self, *args, **kwargs):
        # Print the results
        print args
        print kwargs

        person_id = args[1][1][0][0]
        print "Person ID:", person_id
        # Using the memory. Every event class has it's own memory member variable
        print "Distance:", self.__memory__.getData("PeoplePerception/Person/" + str(person_id) + "/Distance")

    def init(self, glob):
        # Overriding the init function to show how to call proxies. This is optional!
        super(SingleEvent, self).init(glob)  # Always call super with the first argument of your init function.
        # Using proxies. This can be done with get_proxy function or using them as member variables directly. Variable
        # names are defined by the proxy_name string.
        print "Face detection enabled:", self.get_proxy(self.__proxy_name__).isFaceDetectionEnabled()
        # If the string is omitted, the proxy created using the super call is returned.
        print "Detection range:", self.get_proxy().getMaximumDetectionRange()
        # All proxies can be used as a member variables directly
        print "Movement detection:", self.ALPeoplePerception.isMovementDetectionEnabled()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="pepper",
                        help="Robot ip address")
    parser.add_argument("-p", "--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()

    # Create an instance of the class and init the subscription
    s = SingleEvent(
        event="PeoplePerception/PeopleDetected",
        proxy_name="ALPeoplePerception"
    )

    # Start subscribing and keep alive till Ctrl+C is called
    spinner = EventSpinner(
        globals_=globals(),
        ip=args.ip,
        port=args.port,
        events=[s]
    )
    spinner.spin()
