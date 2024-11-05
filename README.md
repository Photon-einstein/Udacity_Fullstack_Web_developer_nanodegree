# Udacity_Fullstack_Web_developer_nanodegree

## Summary
The Full Stack Web Developer Nanodegree program equips students with the essential skills to build and deploy 
dynamic web applications. Through hands-on projects, learners gain proficiency in front-end technologies like 
HTML, CSS, and JavaScript, as well as back-end frameworks such as Flask and SQLAlchemy. 
The curriculum covers RESTful APIs, database management, and deployment strategies, enabling students to create 
robust applications that can handle user interactions and data storage.

## 1 - Project Fyyur

Fyyur is a web application designed to help users discover and manage live music events. Built using Flask and 
SQLAlchemy, this project allows users to create, view, and manage events, as well as register for them. 
The application features user authentication, event filtering, and a responsive design to enhance the user experience. 
Fyyur serves as a practical demonstration of the application of Flask and SQLAlchemy, with creation and managing of a 
database in the backend, ensuring that the data is checked before it is passed to the database.

<img src="0-Media/1-Project_Fyyur_server_running.gif" width="900" height="400" />

## 2 - Trivia App

The Trivia App allows users to play quizzes by answering questions that are organized into different categories. The app provides functionality for:

* Retrieving questions from a PostgreSQL database.
* Filtering questions by category.
* Searching for questions based on keywords.
* Adding new questions.
* Deleting questions.
* Playing a quiz by randomly selecting questions from specific categories.

The backend is developed using Python and Flask, while the database is managed with PostgreSQL.  
The application is designed to follow RESTful API principles and includes unit tests for verifying its functionality.

<img src="0-Media/2-Trivia_App_running.gif" width="900" height="400" />

#include <string>
/*-------------------------------------------------------------------------|
|                         Own Component Includes                           |
|-------------------------------------------------------------------------*/
#include "KNETxDEF/KNETxDEFtyp.hpp"
#include "KNETxLODRxQRYxWRAPPER_lib.hpp"
/*-------------------------------------------------------------------------|
|                       Other Components Includes                          |
|-------------------------------------------------------------------------*/
#include "LODRxTCRxDMD/LODRxTCRxDMD_data_gen_ServiceBundle.hpp"
#include "THXA/THXA_Trace.hpp"

#define CC "KNET"

/** \brief Implementation of convertImageForWaferIdToTaskGenericImageId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertImageForWaferIdToTaskGenericImageId(
   const std::string& image_for_wafer_id)
{
   LODR::Data::iTwinscanCoreDM::ImageForWaferEntityId img_uuid(
      boost::lexical_cast<boost::uuids::uuid>(image_for_wafer_id));
   auto TSCORServiceBundlePtr = LODR::Data::iTwinscanCoreDM::getServiceBundle();
   if(TSCORServiceBundlePtr == nullptr)
   {
      throw std::runtime_error("Unable to get LODR service bundle.");
   }
   std::string tg_image_for_wafer_id = boost::lexical_cast<std::string>(
      TSCORServiceBundlePtr->getReadAccessForImageForWaferReferenceRepo()->get(img_uuid)->getTgImageForWafer());
   THXA_TRACE_ENTRY(KNETxDEF::TRACE_NAME,
                    THXA_TRACE_INT,
                    "image id: %s, tg_image_for_wafer_id: %s",
                    image_for_wafer_id,
                    tg_image_for_wafer_id);
   return tg_image_for_wafer_id;
}

/** \brief Implementation of convertExposureIdToImageForWaferId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertExposureIdToImageForWaferId(const std::string& exposure_id)
{
   auto TSCORServiceBundlePtr = LODR::Data::iTwinscanCoreDM::getServiceBundle();
   if(TSCORServiceBundlePtr == nullptr)
   {
      throw std::runtime_error("Unable to get LODR service bundle.");
   }
   LODR::Data::iTwinscanCoreDM::ExposurePtr lodr_exposure_ptr =
      TSCORServiceBundlePtr->getReadAccessForExposureReferenceRepo()->get(
         LODR::Data::iTwinscanCoreDM::ExposureEntityId(boost::lexical_cast<boost::uuids::uuid>(exposure_id)));
   if(lodr_exposure_ptr == nullptr)
   {
      throw std::runtime_error("Unable to retrieve exposure from LODR.");
   }
   auto img_for_wafer_id = boost::lexical_cast<std::string>(lodr_exposure_ptr->getImage());
   THXA_TRACE_ENTRY(
      KNETxDEF::TRACE_NAME, THXA_TRACE_INT, "Found image_id: %s, for exposure %s", img_for_wafer_id, exposure_id);
   return img_for_wafer_id;
}

/** \brief Implementation of convertTaskGenericExposureIdToTaskGenericImageForWaterId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertTaskGenericExposureIdToTaskGenericImageForWaterId(
   const std::string& tg_exposure_id)
{
   LODR::Data::iTwinscanCoreDM::TaskGenericExposureEntityId lodr_id(
      boost::lexical_cast<boost::uuids::uuid>(tg_exposure_id));
   auto TSCORServiceBundlePtr = LODR::Data::iTwinscanCoreDM::getServiceBundle();
   if(TSCORServiceBundlePtr == nullptr)
   {
      throw std::runtime_error("Unable to get LODR service bundle.");
   }
   auto lodr_exposure = TSCORServiceBundlePtr->getReadAccessForTaskGenericExposureReferenceRepo()->get(lodr_id);
   if(lodr_exposure == nullptr)
   {
      throw std::runtime_error("Unable to retrieve exposure from LODR.");
   }
   std::string tg_image_for_wafer_id = lodr_exposure->getTgImageForWafer().toString();
   THXA_TRACE_ENTRY(KNETxDEF::TRACE_NAME,
                    THXA_TRACE_INT,
                    "KNET LODR Wrapper: Found Task Generic Image For Wafer (%s) for Task Generic Exposure (%s)",
                    tg_image_for_wafer_id,
                    tg_exposure_id);
   return tg_image_for_wafer_id;
}

/** \brief Implementation of convertExposureIdToTaskGenericExposureId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertExposureIdToTaskGenericExposureId(const std::string& exposure_id)
{
   LODR::Data::iTwinscanCoreDM::ExposureEntityId lodr_id(boost::lexical_cast<boost::uuids::uuid>(exposure_id));
   auto TSCORServiceBundlePtr = LODR::Data::iTwinscanCoreDM::getServiceBundle();
   if(TSCORServiceBundlePtr == nullptr)
   {
      throw std::runtime_error("Unable to get LODR service bundle.");
   }
   auto lodr_exposure = TSCORServiceBundlePtr->getReadAccessForExposureReferenceRepo()->get(lodr_id);
   if(lodr_exposure == nullptr)
   {
      throw std::runtime_error("Unable to retrieve exposure from LODR.");
   }
   std::string tg_exposure_id = lodr_exposure->getTgExposure().toString();
   THXA_TRACE_ENTRY(KNETxDEF::TRACE_NAME,
                    THXA_TRACE_INT,
                    "KNTP LODR Wrapper: Found Task Generic Exposure (%s) for Exposure (%s)",
                    tg_exposure_id,
                    exposure_id);
   return tg_exposure_id;
}

/** \brief Implementation of convertTaskGenericImageIdToImageId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertTaskGenericImageIdToImageId(const std::string& tg_image_for_wafer_id)
{
   LODR::Data::iTwinscanCoreDM::TaskGenericImageForWaferEntityId lodr_id(
      boost::lexical_cast<boost::uuids::uuid>(tg_image_for_wafer_id));
   auto TSCORServiceBundlePtr = LODR::Data::iTwinscanCoreDM::getServiceBundle();
   if(TSCORServiceBundlePtr == nullptr)
   {
      throw std::runtime_error("Unable to get LODR service bundle.");
   }
   auto lodr_image_for_wafer =
      TSCORServiceBundlePtr->getReadAccessForTaskGenericImageForWaferReferenceRepo()->get(lodr_id);
   if(lodr_image_for_wafer == nullptr)
   {
      throw std::runtime_error("Unable to retrieve image for wafer from LODR.");
   }
   std::string img_for_wafer_id = lodr_image_for_wafer->getImageId();
   THXA_TRACE_ENTRY(KNETxDEF::TRACE_NAME,
                    THXA_TRACE_INT,
                    "KNET LODR Wrapper: Found Image (%s) for Task Generic Image For Wafer (%s)",
                    img_for_wafer_id,
                    tg_image_for_wafer_id);
   return img_for_wafer_id;
}

/** \brief Implementation of convertTaskGenericExposureIdToImageId()
 */
std::string KNETxLODRxQRYxWRAPPER::Impl::convertTaskGenericExposureIdToImageId(const std::string& tg_exposure_id)
{
   std::string tg_image_for_wafer_id = convertTaskGenericExposureIdToTaskGenericImageForWaterId(tg_exposure_id);
   std::string img_for_wafer_id = convertTaskGenericImageIdToImageId(tg_image_for_wafer_id);
   THXA_TRACE_ENTRY(KNETxDEF::TRACE_NAME,
                    THXA_TRACE_INT,
                    "KNET LODR Wrapper: Found Image (%s) for Task Generic Exposure (%s)",
                    img_for_wafer_id,
                    tg_exposure_id);
   return img_for_wafer_id;
}

