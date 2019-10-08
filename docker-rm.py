import time
import logging
from app.cli import command, arg

def main():
    
    arg.set_vars_from_conf()
    args = arg.get_args()
    
    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    if args.catalog:
        logging.debug("Catalog")
        command.show_catalog()

    elif args.repository:
        logging.debug("Reposirory : {}".format(args.repository))
        command.show_tags(args.repository)

    elif args.dry_run:
        logging.debug("Dry Run:")
        command.dry_run()

    else :
        logging.debug("Delete:")
        command.exec_del(True)


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    logging.debug(f"{__file__} executed in {elapsed:0.2f} seconds.")